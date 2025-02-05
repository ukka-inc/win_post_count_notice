import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as lambdaPython from "@aws-cdk/aws-lambda-python-alpha";
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ENV
    const ENV = scope.node.tryGetContext("ENV");

    // Service Name
    const serviceName = "win-post-count-notice";

    // Slack Channel ID
    let slackChanelId = "";
    switch (ENV) {
      case "dev":
        slackChanelId = "C073A3UBU83";
        break;
      case "prd":
        slackChanelId = "C03RJMDNVP0";
        break;
    }

    // Secrets Manager
    const secretName = `${serviceName}/${ENV}`;
    const secretSlackBotToken = secretsmanager.Secret.fromSecretNameV2(
      this,
      "SLACK_BOT_TOKEN",
      secretName
    );

    // Lambda
    const winPostCountNoticeLambda = new lambdaPython.PythonFunction(
      this,
      `${serviceName}-${ENV}-lambda`,
      {
        functionName: `${ENV}-${serviceName}`,
        runtime: lambda.Runtime.PYTHON_3_12,
        entry: "../app/",
        index: "app_lambda.py",
        handler: "lambda_handler",
        memorySize: 256,
        timeout: cdk.Duration.minutes(3),
        environment: {
          ENV: `${ENV}`,
          SLACK_BOT_TOKEN: `${secretSlackBotToken
            .secretValueFromJson("SLACK_BOT_TOKEN")
            .unsafeUnwrap()}`,
          SLACK_CHANNEL_ID: `${slackChanelId}`,
        },
      }
    );

    // Scheduler
    const rule = new events.Rule(this, `${serviceName}-${ENV}-rule`, {
      ruleName: `${serviceName}-${ENV}-rule`,
      schedule: events.Schedule.cron({
        minute: "55",
        hour: "8",
        weekDay: "FRI",
      }),
    });

    // Add Target
    rule.addTarget(new targets.LambdaFunction(winPostCountNoticeLambda));
  }
}
