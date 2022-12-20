# TeamTailor

This page contains the setup guide and reference information for the Teamtailor source connector.

## Prerequisites

To set up the Teamtailor source connector, you'll need the [API key](https://docs.teamtailor.com/#authentication) with permissions to the resources Airbyte should be able to access.

## Set up the Greenhouse connector in Airbyte

1. [Log into your Airbyte Cloud](https://cloud.airbyte.io/workspaces) account or navigate to the Airbyte Open Source dashboard.
2. Click **Sources** and then click **+ New source**.
3. On the Set up the source page, select **Teamtailor** from the Source type dropdown.
4. Enter the name for the connector.
4. Enter your [**Team-Tailor API Key**](https://docs.teamtailor.com/#authentication) that you obtained from Teamtailor.
5. Click **Set up source**.

## Supported sync modes

The Teamtailor source connector supports the following [sync modes](https://docs.airbyte.com/cloud/core-concepts#connection-sync-modes):

* [Full Refresh - Overwrite](https://docs.airbyte.com/understanding-airbyte/glossary#full-refresh-sync)
* [Full Refresh - Append](https://docs.airbyte.com/understanding-airbyte/connections/full-refresh-append)

For a few streams, like Candidates the use of incremental updates is possible and might be implemented in future versions of the connector.

## Supported Streams
All streams that are theoretically available via the TeamTailor API can be checked in the [API-Documentation](https://docs.teamtailor.com/). From those available the source connector implements the following:

- "candidates"
- "job-applications"
- "jobs"
- "stages"
- "reject-reason"
- "locations"
- "custom-fields"
- "custom-field-values"
- "custom-field-selects"
- "custom-field-options"


## Changelog

| Version | Date       | Pull Request                                             | Subject                                                                        |
|:--------|:-----------|:---------------------------------------------------------|:-------------------------------------------------------------------------------|
| 0.1.0   | NA | NA | Initial Contribution
