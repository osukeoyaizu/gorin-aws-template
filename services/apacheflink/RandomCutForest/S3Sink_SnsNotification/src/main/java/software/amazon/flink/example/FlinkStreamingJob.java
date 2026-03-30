package software.amazon.flink.example;

import software.amazon.flink.example.model.InputData;
import software.amazon.flink.example.model.OutputData;
import software.amazon.flink.example.operator.RandomCutForestOperator;

import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kinesis.FlinkKinesisConsumer;
import org.apache.flink.streaming.connectors.kinesis.config.ConsumerConfigConstants;

// 追加
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;

// S3（行テキストで書く簡易サンプル）
import org.apache.flink.api.common.serialization.SimpleStringEncoder;
import org.apache.flink.core.fs.Path;
import org.apache.flink.streaming.api.functions.sink.filesystem.StreamingFileSink;

// SNS (AWS SDK v2)
import software.amazon.awssdk.services.sns.SnsClient;
import software.amazon.awssdk.services.sns.model.PublishRequest;
import software.amazon.awssdk.regions.Region;

import java.util.Properties;

public class FlinkStreamingJob {

    // ======= 設定 =======
    private static final String REGION = "us-east-1";
    private static final String INPUT_STREAM = "oyaizu";
    private static final String SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:157094121738:oyaizu-sns";
    private static final String S3_SINK_PATH = "s3://oyaizu-kadai-bucket/processed";
    private static final double ANOMALY_THRESHOLD = 3.0;   // スコア閾値
    private static final String OUTPUT_FORMAT = "csv";    // "json" or "csv"
    // =====================

    private static DataStream<InputData> createSource(
            final StreamExecutionEnvironment env,
            final String inputStreamName,
            final String region) {

        Properties inputProps = new Properties();
        inputProps.setProperty(ConsumerConfigConstants.AWS_REGION, region);
        inputProps.setProperty(ConsumerConfigConstants.STREAM_INITIAL_POSITION, "LATEST");

        // DataSerializationSchema は InputData <-> byte[] の変換を実装している想定
        return env.addSource(new FlinkKinesisConsumer<>(
                inputStreamName, new DataSerializationSchema(), inputProps));
    }

    private static StreamingFileSink<String> createS3Sink() {
        return StreamingFileSink
                .forRowFormat(new Path(S3_SINK_PATH), new SimpleStringEncoder<String>("UTF-8"))
                .build();
    }

    private static void sendSnsNotification(OutputData data, String region, String snsTopicArn) {
        try (SnsClient snsClient = SnsClient.builder().region(Region.of(region)).build()) {
            String message = String.format(
                "Anomaly detected: device_id=%s, timestamp=%d, value=%f, is_active=%s, event_id=%s, score=%f",
                data.getDeviceId(), data.getTimestamp(), data.getValue(), data.getIsActive(), data.getEventId(), data.getScore());

            PublishRequest req = PublishRequest.builder()
                    .topicArn(snsTopicArn)
                    .message(message)
                    .build();

            snsClient.publish(req);
        }
    }

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // 1) Kinesis → InputData
        DataStream<InputData> source = createSource(env, INPUT_STREAM, REGION);

        // 2) RCF スコアリング
        RandomCutForestOperator<InputData, OutputData> rcf =
                RandomCutForestOperator.<InputData, OutputData>builder()
                        .setDimensions(1)
                        .setShingleSize(1)
                        .setSampleSize(628)
                        .setInputDataMapper(in -> new float[] { in.getValue() })
                        .setResultMapper((in, score) ->
                                new OutputData(in.getDeviceId(), in.getTimestamp(), in.getValue(), in.getIsActive(), in.getEventId(), score))
                        .build();

        DataStream<OutputData> scored =
                source.process(rcf, TypeInformation.of(OutputData.class)).setParallelism(1);

        // 3) anomaly_flag を付与（score >= 閾値 → 1、それ以外 0）
        DataStream<OutputData> labeled = scored.map(out -> {
            int flag = out.getScore() >= ANOMALY_THRESHOLD ? 1 : 0;
            out.setAnomalyFlag(flag);
            return out;
        });

        // 4) 異常のみ SNS 通知
        labeled
            .filter(out -> out.getAnomalyFlag() == 1)
            .process(new ProcessFunction<OutputData, OutputData>() {
                @Override
                public void processElement(OutputData data, Context ctx, Collector<OutputData> out) {
                    sendSnsNotification(data, REGION, SNS_TOPIC_ARN);
                    out.collect(data); // 流さなくても良ければ削除可
                }
            });

        // 5) S3 へ保存（JSON か CSV を選択）
        if ("csv".equalsIgnoreCase(OUTPUT_FORMAT)) {
            labeled.map(OutputData::toCsvRow)
                   .addSink(createS3Sink());
        } else {
            labeled.map(OutputData::toJsonString) // JSON Lines
                   .addSink(createS3Sink());
        }

        env.execute();
    }
}
