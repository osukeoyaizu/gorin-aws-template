package com.amazonaws.services.msf;

import org.apache.flink.shaded.jackson2.com.fasterxml.jackson.annotation.JsonProperty;

public class Stock {
    // This annotation as well as the associated jackson2 import is needed to correctly map the JSON input key to the
    // appropriate POJO property name to ensure event_time isn't missed in serialization and deserialization
    // @JsonProperty("event_time")
    private float timestamp;
    private float temperature;
    private float humidity;

    public Stock() {}

    public float getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(float timestamp) {
        this.timestamp = timestamp;
    }

    public float getTemperature() {
        return temperature;
    }

    public void setTemperature(float temperature) {
        this.temperature = temperature;
    }

    public float getHumidity() {
        return humidity;
    }

    public void setHumidity(float humidity) {
        this.humidity = humidity;
    }

    @Override
    public String toString() {
        return "Stock{" +
                "timestamp='" + timestamp + '\'' +
                ", temperature='" + temperature + '\'' +
                ", humidity=" + humidity +
                '}';
    }
}
