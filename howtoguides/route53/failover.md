Got it. Since you have two regions and want one failover (primary/secondary), the cleanest approach is to use **two Route53 record sets** for the same name with **failover routing policy**—one marked `PRIMARY` with a health check, and one `SECONDARY` as the fallback. You should use **alias A records** if the targets are ELBs/ALBs (instead of CNAMEs), because those integrate with health evaluation better.

Here’s a self-contained example rewrite:

```hcl
# === variables.tf ===
variable "zone_id" {
  type = string
}

variable "dns_hostname" {
  type = string
}

variable "primary_lb_dns_name" {
  type = string
}

variable "primary_lb_zone_id" {
  type = string
}

variable "secondary_lb_dns_name" {
  type = string
}

variable "secondary_lb_zone_id" {
  type = string
}

# Optional: the health check path for primary (adjust to your app)
variable "primary_health_path" {
  type    = string
  default = "/health"
}

# === health check for primary ===
resource "aws_route53_health_check" "primary" {
  type              = "HTTPS"          # or "HTTP" depending on your listener
  resource_path     = var.primary_health_path
  fqdn              = var.primary_lb_dns_name
  port              = 443              # adjust if not HTTPS
  request_interval  = 30
  failure_threshold = 3
  enable_sni        = true
  # You can tune insufficient_data_health_status if desired:
  insufficient_data_health_status = "Healthy"
}

# === primary (PRIMARY failover) record ===
resource "aws_route53_record" "primary" {
  zone_id = var.zone_id
  name    = var.dns_hostname
  type    = "A"

  set_identifier = "primary"
  failover_routing_policy {
    type = "PRIMARY"
  }

  alias {
    name                   = var.primary_lb_dns_name
    zone_id                = var.primary_lb_zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.primary.id
}

# === secondary (SECONDARY failover) record ===
resource "aws_route53_record" "secondary" {
  zone_id = var.zone_id
  name    = var.dns_hostname
  type    = "A"

  set_identifier = "secondary"
  failover_routing_policy {
    type = "SECONDARY"
  }

  alias {
    name                   = var.secondary_lb_dns_name
    zone_id                = var.secondary_lb_zone_id
    evaluate_target_health = true
  }
}
```

**Key points:**

* The primary record has a health check; if it fails, Route53 fails over to the secondary.
* Both records share the same `name` and `type` but have distinct `set_identifier` and routing policy types.
* Using `alias` A records is preferred for load balancers; you avoid CNAME limitations (e.g., CNAME cannot coexist with other records of same name and doesn’t fit well with failover in some designs).
* Adjust health check settings (`type`, `port`, `resource_path`) to match your service’s actual health endpoint.

If your original architecture was trying to have a “regional” record and a “global” CNAME pointing at it, you can fold that into this failover setup instead—just make the Route53 name itself be the common hostname with the two alias records as above.

Do you want a version of this that wraps into a reusable module with inputs and outputs?
