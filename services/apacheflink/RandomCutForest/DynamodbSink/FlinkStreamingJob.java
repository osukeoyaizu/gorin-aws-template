/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package software.amazon.flink.example;

import software.amazon.flink.example.model.InputData;
import software.amazon.flink.example.model.OutputData;
import software.amazon.flink.example.operator.RandomCutForestOperator;
import com.amazonaws.services.kinesisanalytics.runtime.KinesisAnalyticsRuntime;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.connector.kinesis.sink.KinesisStreamsSink;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kinesis.FlinkKinesisConsumer;
import org.apache.flink.streaming.connectors.kinesis.config.AWSConfigConstants;
import org.apache.flink.streaming.connectors.kinesis.config.ConsumerConfigConstants;

import java.util.Properties;


import org.apache.flink.api.connector.sink2.SinkWriter;
// import org.apache.flink.connector.aws.config.AWSConfigConstants;
import org.apache.flink.connector.base.sink.writer.ElementConverter;
import org.apache.flink.connector.dynamodb.sink.DynamoDbSink;
import org.apache.flink.connector.dynamodb.sink.DynamoDbWriteRequest;
import org.apache.flink.connector.dynamodb.sink.DynamoDbWriteRequestType;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.commons.math3.random.RandomDataGenerator;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;

import java.util.HashMap;
import java.util.Map;

import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;


public class FlinkStreamingJob {
    private static final double ANOMALY_THRESHOLD = 3.0;
    private static String region = "ap-northeast-1";
    private static String table_name = "lab2-dynamodb";
    private static String inputStreamName = "lab2-stream";
    private static DataStream<InputData> createSource(
            final StreamExecutionEnvironment env,
            final String inputStreamName,
            final String region) {
        Properties inputProperties = new Properties();
        inputProperties.setProperty(ConsumerConfigConstants.AWS_REGION, region);

        return env.addSource(new FlinkKinesisConsumer<>(inputStreamName, new DataSerializationSchema(), inputProperties));
    }

    // private static KinesisStreamsSink<OutputData> createSink(final String outputStreamName, final String region) {
    //     Properties outputProperties = new Properties();
    //     outputProperties.setProperty(AWSConfigConstants.AWS_REGION, region);

    //     return KinesisStreamsSink.<OutputData>builder()
    //             .setKinesisClientProperties(outputProperties)
    //             .setSerializationSchema(new DataSerializationSchema())
    //             .setStreamName(outputProperties.getProperty("OUTPUT_STREAM", outputStreamName))
    //             .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))
    //             .build();
    // }
    
    private static DynamoDbSink<OutputData> dynamoDbSink() {
        Properties sinkProperties = new Properties();
        sinkProperties.put(AWSConfigConstants.AWS_REGION, region);
        return DynamoDbSink.<OutputData>builder()
                        .setTableName(table_name)
                        .setElementConverter(new TestDynamoDbElementConverter())
                        .setMaxBatchSize(20)
                        .setDynamoDbProperties(sinkProperties)
                        .build();
    }
    
    public static class TestDynamoDbElementConverter
            implements ElementConverter<OutputData, DynamoDbWriteRequest> {

        private final RandomDataGenerator random = new RandomDataGenerator();

        @Override
        public DynamoDbWriteRequest apply(OutputData outputData, SinkWriter.Context context) {
            final Map<String, AttributeValue> item = new HashMap<>();
            item.put("No", AttributeValue.builder().s(this.random.nextHexString(5)).build());
            item.put("Temp", AttributeValue.builder().s(Float.toString(outputData.getValue())).build());
            item.put("Score", AttributeValue.builder().s(Double.toString(outputData.getScore())).build());

            return DynamoDbWriteRequest.builder()
                    .setType(DynamoDbWriteRequestType.PUT)
                    .setItem(item)
                    .build();
        }
    }

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Properties applicationProperties = KinesisAnalyticsRuntime.getApplicationProperties().get("RcfExampleEnvironment");
        // String region = applicationProperties.getProperty("region", "us-west-2");
        // String inputStreamName = applicationProperties.getProperty("inputStreamName", "ExampleInputStream-RCF");
        // String outputStreamName = applicationProperties.getProperty("outputStreamName", "ExampleOutputStream-RCF");

        DataStream<InputData> source = createSource(env, inputStreamName, region);

        RandomCutForestOperator<InputData, OutputData> randomCutForestOperator =
                RandomCutForestOperator.<InputData, OutputData>builder()
                        .setDimensions(1)
                        .setShingleSize(1)
                        .setSampleSize(628)
                        .setInputDataMapper((inputData) -> new float[]{inputData.getValue()})
                        .setResultMapper(((inputData, score) -> new OutputData(inputData.getTime(), inputData.getValue(), score)))
                        .build();

        source
                .process(randomCutForestOperator, TypeInformation.of(OutputData.class)).setParallelism(1)
                .filter(data -> data.getScore() >= ANOMALY_THRESHOLD)
                .process(new ProcessFunction<OutputData, OutputData>() {
                    @Override
                    public void processElement(OutputData data, Context context, Collector<OutputData> collector) throws Exception {
                        collector.collect(data);
                    }
                })
                .sinkTo(dynamoDbSink());

        env.execute();
    }
}
