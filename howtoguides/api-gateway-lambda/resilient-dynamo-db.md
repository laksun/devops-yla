To configure a **DynamoDB Global Table with multi-region failover** using Terraform (like in your `aws_dynamodb_table` module), you need to:

### ✅ Key Requirements:

1. Use `aws_dynamodb_table` in **each region**.
2. Set the **replica configuration** using the `replica` block.
3. Ensure both tables have the **same name**, **schema**, and **billing mode**.
4. Define provider aliases for each region.

---

### ✅ Steps to Set Up DynamoDB Global Table with Multi-Region (e.g., `us-east-1` and `eu-west-1`):

#### 1. **Define Providers with Aliases**

In your `providers.tf`:

```hcl
provider "aws" {
  alias  = "use1"
  region = "us-east-1"
}

provider "aws" {
  alias  = "euw1"
  region = "eu-west-1"
}
```

---

#### 2. **Update Module to Accept Provider Alias**

In your module call (e.g., in `main.tf` at the root level):

```hcl
module "dynamodb_global_table" {
  source = "./modules/dynamodb"

  providers = {
    aws = aws.use1
  }

  dynamodb_table_name = "my-global-table"
  billing_mode         = "PAY_PER_REQUEST"
  hash_key             = "id"
  config = {
    attributes = [
      {
        name = "id"
        type = "S"
      }
    ]
    global_secondary_indexes = []
  }

  replica_regions = ["eu-west-1"]
}
```

---

#### 3. **Update Your Module to Support Replicas**

In your **`dynamodb/main.tf`** (where you define the table), add:

```hcl
replica {
  for_each = toset(var.replica_regions)
  region_name = each.value
}
```

So your `aws_dynamodb_table` resource becomes:

```hcl
resource "aws_dynamodb_table" "table" {
  provider              = aws
  name                  = var.dynamodb_table_name
  billing_mode          = var.billing_mode
  hash_key              = var.hash_key
  range_key             = try(var.range_key, null)
  stream_enabled        = true
  stream_view_type      = "NEW_AND_OLD_IMAGES"
  table_class           = "STANDARD"
  deletion_protection_enabled = true
  read_capacity         = 0
  write_capacity        = 0

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = var.kms_key_arn
  }

  dynamic "attribute" {
    for_each = var.config.attributes
    content {
      name = attribute.value.name
      type = attribute.value.type
    }
  }

  dynamic "global_secondary_index" {
    for_each = var.config.global_secondary_indexes
    content {
      name               = global_secondary_index.value.name
      hash_key           = global_secondary_index.value.hash_key
      range_key          = try(global_secondary_index.value.range_key, null)
      projection_type    = global_secondary_index.value.projection_type
      non_key_attributes = try(global_secondary_index.value.non_key_attributes, null)
      read_capacity      = lookup(global_secondary_index.value, "read_capacity", 0)
      write_capacity     = lookup(global_secondary_index.value, "write_capacity", 0)
    }
  }

  dynamic "replica" {
    for_each = toset(var.replica_regions)
    content {
      region_name = each.value
    }
  }
}
```

---

#### 4. **Define the `replica_regions` Variable**

In your `variables.tf`:

```hcl
variable "replica_regions" {
  description = "List of regions to replicate the table to"
  type        = list(string)
  default     = []
}
```

---

### 🧪 Optional: Deploy in Multiple Regions for Better Control

If you want full control (e.g., different providers for replicas), you can create two separate tables (in each region) and link them using `replica` configuration. But usually, defining it in one region with `replica` is enough.

---

Would you like me to rewrite your actual module with these changes, or do you want to deploy the same module twice with different providers?
