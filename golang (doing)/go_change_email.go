package main

import (
  "fmt"
  "context"
  // "encoding/json"
  "github.com/aws/aws-lambda-go/lambda"
  // "github.com/aws/aws-lambda-go/events"
  // "io/ioutil"
  // "log"
)

func Handler(ctx context.Context, event string) (string, error) {
  fmt.Printf("Detail = %s\n", event)
  return "abc", nil
}

func main() {
  lambda.Start(Handler)
  // byteValue, err := ioutil.ReadFile("../event.json")
  // if err != nil {
  //   log.Fatal("Error when opening file: ", err)
  // }
  // var payload events.CloudWatchEvent
  // json.Unmarshal(byteValue, &payload)
  // HandleRequest(nil, payload)
}

// GOOS=linux go build -o Handler go_change_email.go
// zip Handler.zip Handler
// aws lambda update-function-code --function-name goChangeEmail --zip-file fileb://./Handler.zip
// aws lambda invoke --function-name goChangeEmail --region us-east-1 response.json