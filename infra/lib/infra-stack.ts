import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as lambdaPython from "@aws-cdk/aws-lambda-python-alpha";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ENV
    const ENV = scope.node.tryGetContext("ENV");

    // Service Name
    const serviceName = "win-post-count-notice";

    // Slack Channel ID
    let slackChaanelId = "";
    switch (ENV) {
      case "dev":
        slackChaanelId = "C073A3UBU83";
        break;
      case "prd":
        slackChaanelId = "C03RJMDNVP0";
        break;
    }

    // Secrets Manager
    const secretName = `${ENV}/${serviceName}`;
    const secretSlackBotToken = secretsmanager.Secret.fromSecretNameV2(
      this,
      "SLACK_BOT_TOKEN",
      secretName
    );

    // Lambda
    new lambdaPython.PythonFunction(this, `${serviceName}-${ENV}-lambda`, {
      functionName: `${ENV}-${serviceName}`,
      runtime: lambda.Runtime.PYTHON_3_12,
      entry: "../app/",
      index: "app_lambda.py",
      handler: "handler",
      memorySize: 256,
      timeout: cdk.Duration.minutes(15),
      environment: {
        ENV: `${ENV}`,
        SLACK_BOT_TOKEN: `${secretSlackBotToken
          .secretValueFromJson("SLACK_BOT_TOKEN")
          .unsafeUnwrap()}`,
      },
    });
  }
}
