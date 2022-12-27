# Event - Lambda - SNS

Sử dụng CloudFormation
- dễ test lambda function
- Handler: index.<function-name>
- Không thể tạo SNS với số lượng subscription tùy ý

Sử dụng Terraform
- handler = "<file-name>.<function-name>"
- Tạo SNS với số lượng subscription tùy ý
