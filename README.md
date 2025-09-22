# fmu-datamodels

This package contains models and schemas that contribute to the FMU data
standard.

Data is represented using Pydantic models, which describe metadata for data
exported from FMU experiments. These models can be serialized into versioned
[JSON schemas](https://json-schema.org/) that validate the metadata. In some
cases the exported data itself can be validated by a schema contained here.

The models are utilized by [fmu-dataio](https://github.com/equinor/fmu-dataio)
for data export and can also be leveraged by Sumo data consumers for
programmatic access to data model values like enumerations.

## Schemas

The metadata standard is defined by [JSON schemas](https://json-schema.org/).
Within Equinor, the schemas are available on a Radix-hosted endpoint.

- Radix Dev: ![Radix
  Dev](https://api.radix.equinor.com/api/v1/applications/fmu-schemas/environments/dev/buildstatus)
- Radix Staging: ![Radix
  Staging](https://api.radix.equinor.com/api/v1/applications/fmu-schemas/environments/staging/buildstatus)
- Radix Prod: ![Radix
  Prod](https://api.radix.equinor.com/api/v1/applications/fmu-schemas/environments/prod/buildstatus)

## Documentation

The documentation for this package is built into the
[fmu-dataio](https://fmu-dataio.readthedocs.io/en/latest/) documentation.

- The [FMU results data
  model](https://fmu-dataio.readthedocs.io/en/latest/datamodel/index.html)
  page documents the data model, contains the schema change logs, and more.
- The [Schema
  versioning](https://fmu-dataio.readthedocs.io/en/latest/schema_versioning.html)
  page describes how schemas produced by this model are versioned.
- The [Updating
  schemas](https://fmu-dataio.readthedocs.io/en/latest/update_schemas.html)
  page contains instructions on how to update the schemas. This is relevant
  for developers of this model only.

## License

This project is licensed under the terms of the [Apache
2.0](https://github.com/equinor/fmu-datamodels/blob/main/LICENSE) license.
