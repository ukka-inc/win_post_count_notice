#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { InfraStack } from "../lib/infra-stack";

const app = new cdk.App();
const ENV = process.env.ENV;
new InfraStack(app, `win-post-count-notice-stack-${ENV}`, {
  stackName: `win-post-count-notice-stack-${ENV}`,
});
