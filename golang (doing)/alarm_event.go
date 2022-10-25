package main

import (
  "time"
)

type Event struct {
  Version    string    `json:"version"`
  ID         string    `json:"id"`
  DetailType string    `json:"detail-type"`
  Source     string    `json:"source"`
  Account    string    `json:"account"`
  Time       time.Time `json:"time"`
  Region     string    `json:"region"`
  Resources  []string  `json:"resources"`
  Detail     struct {
    AlarmName string `json:"alarmName"`
    State     struct {
      Value      string `json:"value"`
      Reason     string `json:"reason"`
      ReasonData string `json:"reasonData"`
      Timestamp  string `json:"timestamp"`
    } `json:"state"`
    PreviousState struct {
      Value      string `json:"value"`
      Reason     string `json:"reason"`
      ReasonData string `json:"reasonData"`
      Timestamp  string `json:"timestamp"`
    } `json:"previousState"`
    Configuration struct {
      Metrics []struct {
        ID         string `json:"id"`
        MetricStat struct {
          Metric struct {
            Namespace  string `json:"namespace"`
            Name       string `json:"name"`
            Dimensions struct {
              InstanceID string `json:"InstanceId"`
            } `json:"dimensions"`
          } `json:"metric"`
          Period int    `json:"period"`
          Stat   string `json:"stat"`
        } `json:"metricStat"`
        ReturnData bool `json:"returnData"`
      } `json:"metrics"`
      Description string `json:"description"`
    } `json:"configuration"`
  } `json:"detail"`
}
