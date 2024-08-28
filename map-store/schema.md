## `sbml_info` table

| Field Name       | Data Type | Description                                | Example Value                                                 |
|------------------|-----------|--------------------------------------------|---------------------------------------------------------------|
| id               | Integer   | Primary key, auto-incremented              | Auto-incremented                                              |
| xmlns            | String    | XML namespace                              | `http://www.sbml.org/sbml/level3/version2/core`               |
| layout_required  | String    | Indicates if layout is required            | `false`                                                       |
| level            | Integer   | SBML level                                 | `3`                                                           |
| multi_required   | String    | Indicates if multi-part is required        | `true`                                                        |
| render_required  | String    | Indicates if rendering is required         | `false`                                                       |
| version          | Integer   | Version number                             | `2`                                                           |
| xmlns_layout     | String    | XML namespace for layout                   | `http://www.sbml.org/sbml/level3/version1/layout/version1`    |
| xmlns_multi      | String    | XML namespace for multi-part               | `http://www.sbml.org/sbml/level3/version1/multi/version1`     |
| xmlns_render     | String    | XML namespace for rendering                | `http://www.sbml.org/sbml/level3/version1/render/version1`    |

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


## `layouts` table

### `layouts_info` table
| Field Name | Data Type | Description           | Example Value   |
|------------|-----------|-----------------------|-----------------|
| model_id   | String    | Foreign key to Model Table | `new_PPP`      |
| layout_id  | String    | Unique identifier for the layout | `layout_1`    |
| height     | Float     | Height of the layout  | `500.0`         |
| width      | Float     | Width of the layout   | `800.0`         |


### `color_definitions` table
| Field Name    | Data Type | Description           | Example Value   |
|---------------|-----------|-----------------------|-----------------|
| model_id      | String    | Foreign key to Model Table | `new_PPP`      |
| color_id      | String    | Unique identifier for the color | `color_1`      |
| render_info_id| String    | Foreign key to Render Information Table | `render_1`  |
| color_value   | String    | Color value (e.g., "#FFFFFF")    | `#FFFFFF`      |


### `line_endings` table
| Field Name    | Data Type | Description                           | Example Value        |
|---------------|-----------|---------------------------------------|----------------------|
| model_id      | String    | Foreign key to Model Table            | `new_PPP`            |
| line_ending_id| String    | Unique identifier for the line ending | `line_ending_FULL`   |
| fill          | String    | Fill color of the graphic element     | `color_FF000000`     |
| position_x    | Float     | X position of the bounding box        | `-12`                |
| position_y    | Float     | Y position of the bounding box        | `-6`                 |
| position_z    | Float     | Z position of the bounding box        | `0`                  |
| height        | Float     | Height of the bounding box            | `12`                 |
| width         | Float     | Width of the bounding box             | `12`                 |


### `line_endings_glyphs` table
| Field Name      | Data Type | Description                                  | Example Value        |
|-----------------|-----------|----------------------------------------------|----------------------|
| graphic_id      | String    | Unique identifier for each graphic element   | `graphic_1`          |
| line_ending_id  | String    | Foreign key to Line Endings Table            | `line_ending_FULL`   |
| element_type    | String    | Type of graphic element                      | `RenderPoint`        |
| x               | String    | X coordinate of the graphic element          | `0`, `100%`          |
| y               | String    | Y coordinate of the graphic element          | `0`, `50%`, `100%`   |

### `style` table
| Field Name  | Data Type | Description                           | Example Value  |
|-------------|-----------|---------------------------------------|----------------|
| model_id    | String    | Foreign key to Model Table            | `new_PPP`      |
| style_id    | String    | Unique identifier for the style       | `style_sa40`   |
| id_list     | String    | List of identifiers this style applies to | `sa40`      |
| is_text     | Boolean   | Indicates if the style is for text (true if idList starts with 'text_') | `false`       |
| render_info_id | String | Foreign key to Render Information Table | `render_1`    |

### `style_glyphs` table
| Field Name    | Data Type | Description                                | Example Value   |
|---------------|-----------|--------------------------------------------|-----------------|
| style_graphic_id | String  | Unique identifier for the graphic setting  | `graphic_1`     |
| style_id      | String    | Foreign key to Styles Table                | `style_sa40`    |
| fill          | String    | Fill color                                 | `color_FFCCFF66`|
| stroke        | String    | Stroke color                               | `color_FF000000`|
| stroke_width  | String    | Stroke width                               | `1`             |
| font_size     | String    | Font size (only if is_text is true)        | `12`            |
| text_anchor   | String    | Text anchor position (only if is_text is true) | `middle`    |
| vtext_anchor  | String    | Vertical text anchor position (only if is_text is true) | `middle` |


### `style_polygon` table

| Field Name     | Data Type | Description                                  | Example Value   |
|----------------|-----------|----------------------------------------------|-----------------|
| polygon_id     | String    | Unique identifier for the polygon            | `polygon_1`     |
| style_graphic_id| String   | Foreign key to Style Graphics Table          | `graphic_1`     |


### `polygon_elements` table
| Field Name     | Data Type | Description                         | Example Value   |
|----------------|-----------|-------------------------------------|-----------------|
| element_id     | String    | Unique identifier for the element   | `element_1`     |
| polygon_id     | String    | Foreign key to Style Polygon Table  | `polygon_1`     |
| x              | Integer   | X coordinate of the point           | `348`           |
| y              | Integer   | Y coordinate of the point           | `1020`          |
| xsi_type       | String    | Type of the render point            | `RenderPoint`   |


### `style_shape_specifics` table
| Field Name   | Data Type | Description                            | Example Value |
|--------------|-----------|----------------------------------------|---------------|
| shape_id     | String    | Unique identifier for the shape        | `ellipse_1`   |
| style_id     | String    | Foreign key to Styles Table            | `style_sa40`  |
| cx           | String    | Center x-coordinate of the ellipse     | `50%`         |
| cy           | String    | Center y-coordinate of the ellipse     | `50%`         |
| rx           | String    | Radius x of the ellipse                | `50%`         |
| ry           | String    | Radius y of the ellipse                | `50%`         |

### `compartment_glyphs` table
| Field Name        | Data Type | Description                             | Example Value        |
|-------------------|-----------|-----------------------------------------|----------------------|
| model_id          | String    | Foreign key to Model Table              | `new_PPP`            |
| glyph_id          | String    | Unique identifier for the glyph         | `default_compartment`|
| compartment_id    | String    | Identifier of the related compartment   | `default`            |
| layout_id         | String    | Foreign key to Layouts Table            | `layout_1`           |
| position_x        | Float     | X coordinate of the glyph's position    | `0`                  |
| position_y        | Float     | Y coordinate of the glyph's position    | `0`                  |
| position_z        | Float     | Z coordinate of the glyph's position    | `0`                  |
| width             | Float     | Width of the glyph                      | `1491`               |
| height            | Float     | Height of the glyph                     | `1128`               |

### `species_glyphs` table
| Field Name     | Data Type | Description                               | Example Value     |
|----------------|-----------|-------------------------------------------|-------------------|
| model_id       | String    | Foreign key to Model Table                | `new_PPP`         |
| glyph_id       | String    | Unique identifier for the glyph           | `sa40`            |
| species_id     | String    | Identifier of the related species         | `species_0`       |
| layout_id      | String    | Foreign key to Layouts Table              | `layout_1`        |
| position_x     | Float     | X coordinate of the glyph's position      | `922.6666666667`  |
| position_y     | Float     | Y coordinate of the glyph's position      | `732.6666666667`  |
| position_z     | Float     | Z coordinate of the glyph's position      | `27`              |
| width          | Float     | Width of the glyph                        | `70`              |
| height         | Float     | Height of the glyph                       | `25`              |


### `reaction_glyphs` table
| Field Name      | Data Type | Description                              | Example Value  |
|-----------------|-----------|------------------------------------------|----------------|
| model_id        | String    | Foreign key to Model Table               | `new_PPP`      |
| reaction_glyph_id | String   | Unique identifier for the reaction glyph | `re10_0`       |
| reaction_id     | String    | Identifier of the related reaction       | `re10`         |
| layout_id       | String    | Foreign key to Layouts Table             | `layout_1`     |

### `reaction_glyphs_curve` table
| Field Name      | Data Type | Description                              | Example Value     |
|-----------------|-----------|------------------------------------------|-------------------|
| model_id        | String    | Foreign key to Model Table               | `new_PPP`         |
| reaction_glyph_id | String   | Foreign key to Reaction Glyphs Table     | `re10_0`          |
| segment_id      | String    | Unique identifier for the curve segment  | `segment_1`       |
| reaction_glyph_id | String  | Foreign key to Reaction Glyphs Table     | `re10_0`          |
| type            | String    | Type of the segment, e.g., "LineSegment" | `LineSegment`     |
| start_x         | Float     | X coordinate of the start point          | `516.1767443144`  |
| start_y         | Float     | Y coordinate of the start point          | `642.5000137966`  |
| start_z         | Float     | Z coordinate of the start point          | `0`               |
| end_x           | Float     | X coordinate of the end point            | `515.8232556856`  |
| end_y           | Float     | Y coordinate of the end point            | `604.4999862034`  |
| end_z           | Float     | Z coordinate of the end point            | `0`               |

### `reaction_glyphs_species_reference` table
| Field Name          | Data Type | Description                                 | Example Value  |
|---------------------|-----------|---------------------------------------------|----------------|
| model_id            | String    | Foreign key to Model Table                  | `new_PPP`      |
| reaction_glyph_id    | String   | Foreign key to Reaction Glyphs Table        | `re10_0`       |
| species_ref_glyph_id | String   | Unique identifier for the species reference glyph | `node_1`    |
| species_glyph_id     | String   | Identifier of the related species glyph     | `sa19`         |
| role                 | String   | Role of the species in the reaction, e.g., "substrate" | `substrate` |

### `reaction_species_reference_curve` table
| Field Name      | Data Type | Description                              | Example Value                |
|-----------------|-----------|------------------------------------------|------------------------------|
| model_id        | String    | Foreign key to Model Table               | `new_PPP`                    |
| reaction_glyph_id | String   | Foreign key to Reaction Glyphs Table     | `re10_0`                     |
| species_ref_glyph_id | String  | Foreign key to Species Reference Glyphs Table | `node_1`             |
| segment_id      | String    | Unique identifier for the curve segment  | `segment_1001`              |
| type            | String    | Type of the segment, e.g., "LineSegment" | `LineSegment`               |
| start_x         | Float     | X coordinate of the start point          | `16046.5`                   |
| start_y         | Float     | Y coordinate of the start point          | `22080.0`                   |
| start_z         | Float     | Z coordinate of the start point          | `498`                       |
| end_x           | Float     | X coordinate of the end point            | `16520`                     |
| end_y           | Float     | Y coordinate of the end point            | `22100.0`                   |
| end_z           | Float     | Z coordinate of the end point            | `498`                       |


### `text_glyphs` table
| Field Name         | Data Type | Description                               | Example Value      |
|--------------------|-----------|-------------------------------------------|--------------------|
| model_id           | String    | Foreign key to Model Table                | `new_PPP`          |
| text_glyph_id      | String    | Unique identifier for the text glyph      | `text_sa40`        |
| graphical_object_id| String    | Identifier of the related graphical object| `sa40`             |
| layout_id          | String    | Foreign key to Layouts Table              | `layout_1`         |
| text               | String    | Text content of the glyph                 | `e4p_c`            |
| position_x         | Float     | X coordinate of the glyph's position      | `922.6666666667`   |
| position_y         | Float     | Y coordinate of the glyph's position      | `732.6666666667`   |
| position_z         | Float     | Z coordinate of the glyph's position      | `28`               |
| width              | Float     | Width of the glyph                        | `70`               |
| height             | Float     | Height of the glyph                       | `25`               |