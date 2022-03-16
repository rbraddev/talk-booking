import argparse

import boto3


def get_zone_id(client, domain_name: str) -> str:
    zones = client.list_hosted_zones()
    try:
        zone_id = next(
            zone["Id"]
            for zone in zones["HostedZones"]
            if zone["Name"] == f"{domain_name}."
        )
    except StopIteration:
        raise ValueError(f"Domain name {domain_name} not found")
    return zone_id


def get_record_set(client, zone_id: str) -> list(dict):
    record_sets = client.list_resource_record_sets(HostedZoneId=zone_id)[
        "ResourceRecordSets"
    ]
    try:
        record_set = next(
            rs["ResourceRecords"] for rs in record_sets if rs["Type"] == "NS"
        )
    except StopIteration:
        raise ValueError("Unable to find NS Record Set")
    return [{"Name": record["Value"]} for record in record_set]


def update_domain_record_set(client, domain_name: str, record_set: list(dict)) -> None:
    response = client.update_domain_nameservers(
        DomainName=domain_name, Nameservers=record_set
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print("Name Servers Updated!")
    else:
        raise Exception("Unable to update Name Servers")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="Name of Hosted Domain")

    args = parser.parse_args()
    domain_name = args.domain

    route53_client = boto3.client("route53")
    route53domains_client = boto3.client("route53domains", region_name="us-east-1")

    zone_id = get_zone_id(route53_client, domain_name)
    record_set = get_record_set(route53_client, zone_id)
    update_domain_record_set(route53domains_client, domain_name, record_set)
