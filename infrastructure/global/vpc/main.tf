terraform {
  backend "s3" {
    bucket = "talk-booking-terraform"
    key = "terraform/tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = var.region
}