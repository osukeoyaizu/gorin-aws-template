package com.amazonaws.services.msf;

import com.amazonaws.services.kinesisanalytics.runtime.KinesisAnalyticsRuntime;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.connector.kinesis.sink.KinesisStreamsSink;
import org.apache.flink.connector.kinesis.source.KinesisStreamsSource;
import org.apache.flink.formats.json.JsonDeserializationSchema;
import org.apache.flink.formats.json.JsonSerializationSchema;
import org.apache.flink.shaded.guava31.com.google.common.collect.Maps;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.LocalStreamEnvironment;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Map;
import java.util.Properties;


// DynamoDB Sink 用
import org.apache.flink.api.connector.sink2.SinkWriter;
import org.apache.flink.connector.aws.config.AWSConfigConstants;
import org.apache.flink.connector.base.sink.writer.ElementConverter;
import org.apache.flink.connector.dynamodb.sink.DynamoDbSink;
import org.apache.flink.connector.dynamodb.sink.DynamoDbWriteRequest;
import org.apache.flink.connector.dynamodb.sink.DynamoDbWriteRequestType;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;


// その他
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;

import java.util.HashMap;
import java.util.UUID;
import java.util.Map;

import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;


public class StreamingJob {
    private static final Logger LOG = LoggerFactory.getLogger(StreamingJob.class);

    // Name of the local JSON resource with the application properties in the same format as they are received from the Amazon Managed Service for Apache Flink runtime
    private static final String LOCAL_APPLICATION_PROPERTIES_RESOURCE = "flink-application-properties-dev.json";

    private static String region = "ap-northeast-1";
    private static String table_name = "lab1-table";

    private static boolean isLocal(StreamExecutionEnvironment env) {
        return env instanceof LocalStreamEnvironment;
    }

    /**
     * Load application properties from Amazon Managed Service for Apache Flink runtime or from a local resource, when the environment is local
     */
    private static Map<String, Properties> loadApplicationProperties(StreamExecutionEnvironment env) throws IOException {
        if (isLocal(env)) {
            LOG.info("Loading application properties from '{}'", LOCAL_APPLICATION_PROPERTIES_RESOURCE);
            return KinesisAnalyticsRuntime.getApplicationProperties(
                    StreamingJob.class.getClassLoader()
                            .getResource(LOCAL_APPLICATION_PROPERTIES_RESOURCE).getPath());
        } else {
            LOG.info("Loading application properties from Amazon Managed Service for Apache Flink");
            return KinesisAnalyticsRuntime.getApplicationProperties();
        }
    }

    private static <T> KinesisStreamsSource<T> createKinesisSource(Properties inputProperties, final DeserializationSchema<T> deserializationSchema) {
        final String inputStreamArn = inputProperties.getProperty("stream.arn");
        return KinesisStreamsSource.<T>builder()
                .setStreamArn(inputStreamArn)
                .setSourceConfig(Configuration.fromMap(Maps.fromProperties(inputProperties)))
                .setDeserializationSchema(deserializationSchema)
                .build();
    }

    // private static <T> KinesisStreamsSink<T> createKinesisSink(Properties outputProperties, final SerializationSchema<T> serializationSchema) {
    //     final String outputStreamArn = outputProperties.getProperty("stream.arn");
    //     return KinesisStreamsSink.<T>builder()
    //             .setStreamArn(outputStreamArn)
    //             .setKinesisClientProperties(outputProperties)
    //             .setSerializationSchema(serializationSchema)
    //             .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))
    //             .build();
    // }
    
    private static DynamoDbSink<Stock> dynamoDbSink() {
        Properties sinkProperties = new Properties();
        sinkProperties.put(AWSConfigConstants.AWS_REGION, region);
        return DynamoDbSink.<Stock>builder()
                        .setTableName(table_name)
                        .setElementConverter(new TestDynamoDbElementConverter())
                        .setMaxBatchSize(20)
                        .setDynamoDbProperties(sinkProperties)
                        .build();
    }
    
    public static class TestDynamoDbElementConverter
            implements ElementConverter<Stock, DynamoDbWriteRequest> {
        @Override
        public DynamoDbWriteRequest apply(Stock stock, SinkWriter.Context context) {
            final Map<String, AttributeValue> item = new HashMap<>();
            item.put("id", AttributeValue.builder().s(UUID.randomUUID().toString()).build());
            item.put("timestamp", AttributeValue.builder().n(String.valueOf(stock.getTimestamp())).build());
            item.put("spot", AttributeValue.builder().s(stock.getSpot()).build());
            item.put("temperature", AttributeValue.builder().s(Double.toString(stock.getTemperature())).build());
            item.put("humidity", AttributeValue.builder().s(Float.toString(stock.getHumidity())).build());
            item.put("isActive", AttributeValue.builder().s(Boolean.toString(stock.getIsActive())).build());
            
            return DynamoDbWriteRequest.builder()
                    .setType(DynamoDbWriteRequestType.PUT)
                    .setItem(item)
                    .build();
        }
    }

    public static void main(String[] args) throws Exception {
        // set up the streaming execution environment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        final Map<String, Properties> applicationProperties = loadApplicationProperties(env);
        LOG.warn("Application properties: {}", applicationProperties);

        KinesisStreamsSource<Stock> source = createKinesisSource(applicationProperties.get("InputStream0"), new JsonDeserializationSchema<>(Stock.class));

        DataStream<Stock> input = env.fromSource(source,
                WatermarkStrategy.noWatermarks(),
                "Kinesis source",
                TypeInformation.of(Stock.class));

        // // temperatureが30.0以上のデータのみフィルタリング
        // DataStream<Stock> filtered = input.filter(stock -> stock.getTemperature() >= 30.0);
        // filtered.sinkTo(dynamoDbSink());

        input.sinkTo(dynamoDbSink());
        env.execute("Flink Kinesis Source and Sink examples");
    }
}
