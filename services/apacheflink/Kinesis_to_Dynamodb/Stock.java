package com.amazonaws.services.msf;

import org.apache.flink.shaded.jackson2.com.fasterxml.jackson.annotation.JsonProperty;

public class Stock {
    // This annotation as well as the associated jackson2 import is needed to correctly map the JSON input key to the
    // appropriate POJO property name to ensure event_time isn't missed in serialization and deserialization
    @JsonProperty("EVENT_TIME")
    private int timestamp;
    @JsonProperty("SPOT")
    private String spot;
    @JsonProperty("TEMPERATURE")
    private double temperature;
    @JsonProperty("HUMIDITY")
    private float humidity;
    @JsonProperty("IS_ACTIVE")
    private boolean isActive;

    public Stock() {}

    public int getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(int timestamp) {
        this.timestamp = timestamp;
    }

    public String getSpot() {
        return spot;
    }

    public void setSpot(String spot) {
        this.spot = spot;
    }

    public double getTemperature() {
        return temperature;
    }

    public void setTemperature(double temperature) {
        this.temperature = temperature;
    }

    public float getHumidity() {
        return humidity;
    }

    public void setHumidity(float humidity) {
        this.humidity = humidity;
    }

    public boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(boolean isActive) {
        this.isActive = isActive;
    }

    @Override
    public String toString() {
        return "Stock{" +
                "EVENT_TIME='" + timestamp + '\'' +
                ", SPOT='" + spot + '\'' +
                ", TEMPERATURE='" + temperature + '\'' +
                ", HUMIDITY='" + humidity + '\'' +
                ", IS_ACTIVE=" + isActive +
                '}';
    }
}
