## `sbml_info` table

| Field Name       | Data Type | Description                                                          | Example Value                                                 |
|------------------|-----------|----------------------------------------------------------------------|---------------------------------------------------------------|
| id               | Integer   | Primary key, auto-incremented                                        | Auto-incremented                                              |
| xmlns            | String    | XML namespace                                                        | `http://www.sbml.org/sbml/level3/version2/core`               |
| layout_required  | String    | Indicates if layout is required                                      | `false`                                                       |
| level            | Integer   | SBML level                                                           | `3`                                                           |
| multi_required   | String    | Indicates if multi-part is required                                  | `true`                                                        |
| render_required  | String    | Indicates if rendering is required                                   | `false`                                                       |
| version          | Integer   | Version number                                                       | `2`                                                           |
| xmlns_layout     | String    | XML namespace for layout                                             | `http://www.sbml.org/sbml/level3/version1/layout/version1`    |
| xmlns_multi      | String    | XML namespace for multi-part                                         | `http://www.sbml.org/sbml/level3/version1/multi/version1`     |
| xmlns_render     | String    | XML namespace for rendering                                          | `http://www.sbml.org/sbml/level3/version1/render/version1`    |

## `model` table

### `model_info` table
| Field Name        | Data Type | Description                        | Example Value      |
|-------------------|-----------|------------------------------------|--------------------|
| id                | String    | Unique identifier for the model    | `new_PPP`          |
| area_units        | String    | Units of area used in the model    | `area`             |
| extent_units      | String    | Units of extent used in the model  | `mole`             |
| length_units      | String    | Units of length used in the model  | `metre`            |
| substance_units   | String    | Units of substance used in the model | `mole`           |
| time_units        | String    | Units of time used in the model    | `second`           |
| volume_units      | String    | Units of volume used in the model  | `litre`            |

### `model_notes` table

| Field Name | Data Type | Description             | Example Value                  |
|------------|-----------|-------------------------|--------------------------------|
| xmlns      | String    | XML namespace for notes | `http://www.w3.org/1999/xhtml` |
| content    | Text      | Content of the note     | `null`                         |

### `model_rdf_namespace` table

| Field Name    | Data Type | Description                  | Example Value                                |
|---------------|-----------|------------------------------|----------------------------------------------|
| rdf           | String    | RDF namespace                | `http://www.w3.org/1999/02/22-rdf-syntax-ns#`|
| dcterms_modified     | String    | Fixed value indicating the RDF parse type of modification | `"@rdf:parseType": "Resource"`         |
| dc            | String    | Dublin Core namespace        | `http://purl.org/dc/elements/1.1/`           |
| dcterms       | String    | Dublin Core Terms namespace  | `http://purl.org/dc/terms/`                  |
| vCard         | String    | vCard RDF namespace          | `http://www.w3.org/2001/vcard-rdf/3.0#`      |
| bqbiol        | String    | Biology qualifier namespace  | `http://biomodels.net/biology-qualifiers/`   |
| bqmodel       | String    | Model qualifier namespace    | `http://biomodels.net/model-qualifiers/`     |

## `list_species_types` table

### `species_type` table
| Field Name | Data Type | Description                     | Example Value |
|------------|-----------|---------------------------------|---------------|
| model_id   | String    | Foreign key linked to Model Table | `new_PPP`    |
| species_type_id | String | Unique identifier for the species type | `sp1`        |
| name       | String    | Name of the species type        | `speciesName` |
| sbo_term   | String    | SBO term for the species type   | `SBO:0000243` |


### `species_feature_type` table
| Field Name | Data Type | Description                        | Example Value |
|------------|-----------|------------------------------------|---------------|
| feature_type_id | String | Unique identifier for the feature type | `ft1`       |
| species_type_id | String | Foreign key to Species Types Table | `sp1`        |
| name       | String    | Name of the feature type           | `featureName`|
| occur      | String    | Occurrence info of the feature type| `optional`   |

### `possible_species_feature_values` table
| Field Name | Data Type | Description                        | Example Value |
|------------|-----------|------------------------------------|---------------|
| value_id   | String    | Unique identifier for the value    | `val1`        |
| feature_type_id | String | Foreign key to Species Feature Types Table | `ft1`  |
| name       | String    | Name of the possible value         | `valueName`   |


## `unit_definiton` table 

### `unit_definitions` table
| Field Name | Data Type | Description              | Example Value |
|------------|-----------|--------------------------|---------------|
| model_id   | String    | Foreign key linked to Model Table | `new_PPP`  |
| unit_id    | String    | Unique identifier for the unit definition | `time`       |
| name       | String    | Name of the unit definition   | `time`       |


### `units` table
| Field Name | Data Type | Description                 | Example Value |
|------------|-----------|-----------------------------|---------------|
| unit_id    | String    | Foreign key linked to Unit Definitions Table | `time`     |
| exponent   | Integer   | Exponent of the unit        | `1`           |
| kind       | String    | Kind of unit (e.g., second, metre, mole) | `second`    |
| multiplier | Integer   | Multiplier of the unit      | `1`           |
| scale      | Integer   | Scale of the unit           | `0`           |


## `Compartments` table

### `compartment` table
| Field Name         | Data Type | Description                         | Example Value  |
|--------------------|-----------|-------------------------------------|----------------|
| model_id           | String    | Foreign key linked to Model Table   | `new_PPP`      |
| compartment_id     | String    | Unique identifier for the compartment | `default`     |
| constant           | Boolean   | Whether the compartment size is constant | `false`      |
| is_type            | Boolean   | Whether the compartment is a type   | `false`        |
| size               | Float     | Size of the compartment             | `1`            |
| spatial_dimensions | Integer   | Spatial dimensions of the compartment | `3`           |


## `list_species` table

### `species` table
| Field Name               | Data Type | Description                                      | Example Value                  |
|--------------------------|-----------|--------------------------------------------------|--------------------------------|
| model_id                 | String    | Foreign key linked to Model Table                | `new_PPP`                      |
| species_id               | String    | Unique identifier for the species                | `species_0`                    |
| boundary_condition       | Boolean   | Indicates if the species has a boundary condition| `false`                        |
| compartment              | String    | Compartment in which the species is located      | `default`                      |
| constant                 | Boolean   | Indicates if the species amount is constant      | `false`                        |
| has_only_substance_units | Boolean   | Indicates if the species uses only substance units | `false`                      |
| initial_amount           | Float     | Initial amount of the species                    | `0`                            |
| multi_species_type       | String    | Type of species in multi-namespace              | `minerva_species_type_SimpleMolecule` |
| name                     | String    | Name of the species                              | `e4p_c`                        |
| sbo_term                 | String    | Systems Biology Ontology term for the species    | `SBO:0000247`                  |

### `species_features` table
| Field Name             | Data Type | Description                              | Example Value                                        |
|------------------------|-----------|------------------------------------------|------------------------------------------------------|
| feature_id             | String    | Unique identifier for the species feature| `feature_001`                                        |
| species_id             | String    | Foreign key linked to Species Table      | `species_0`                                          |
| occur                  | Integer   | Occurrence information of the feature    | `1`                                                  |
| species_feature_type   | String    | Type of the species feature              | `minerva_position_to_compartment_SimpleMolecule`     |


### `species_feature_values` table
| Field Name             | Data Type | Description                            | Example Value                                        |
|------------------------|-----------|----------------------------------------|------------------------------------------------------|
| feature_value_id       | String    | Unique identifier for the feature value| `value_001`                                          |
| feature_id             | String    | Foreign key linked to Species Features Table | `feature_001`                             |
| value                  | String    | The value assigned to the feature      | `minerva_position_to_compartment_SimpleMolecule_53`  |

## `list_reactions` table

### `reaction` table
| Field Name   | Data Type | Description                           | Example Value       |
|--------------|-----------|---------------------------------------|---------------------|
| reaction_id  | String    | Unique identifier for the reaction    | `re10`              |
| name         | String    | Name of the reaction                  | `PGL`               |
| reversible   | Boolean   | Indicates if the reaction is reversible | `false`           |
| sbo_term     | String    | Systems Biology Ontology term for the reaction | `SBO:0000176` |


### `reaction_reactants` table
| Field Name    | Data Type | Description                            | Example Value   |
|---------------|-----------|----------------------------------------|-----------------|
| id            | String    | Unique identifier for the reactant     | `reactant_001`  |
| reaction_id   | String    | Foreign key to Reactions Table         | `re10`          |
| species_id    | String    | Identifier of the species involved     | `species_12`    |
| constant      | Boolean   | Indicates if the species amount is constant | `false`     |


### `reaction_products` table
| Field Name    | Data Type | Description                            | Example Value   |
|---------------|-----------|----------------------------------------|-----------------|
| id            | String    | Unique identifier for the product      | `product_001`   |
| reaction_id   | String    | Foreign key to Reactions Table         | `re10`          |
| species_id    | String    | Identifier of the species involved     | `species_22`    |
| constant      | Boolean   | Indicates if the species amount is constant | `false`     |
