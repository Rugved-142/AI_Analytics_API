variable "project_name" { type = string }
variable "private_subnet_ids" { type = list(string) }
variable "vpc_id" { type = string }

resource "aws_security_group" "msk" {
  name   = "${var.project_name}-msk-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 9092
    to_port     = 9098
    protocol    = "tcp"
    cidr_blocks = ["10.20.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_msk_cluster" "this" {
  cluster_name           = "${var.project_name}-msk"
  kafka_version          = "3.7.x"
  number_of_broker_nodes = 2

  broker_node_group_info {
    instance_type   = "kafka.t3.small"
    client_subnets  = var.private_subnet_ids
    security_groups = [aws_security_group.msk.id]
  }
}

output "bootstrap_brokers" { value = aws_msk_cluster.this.bootstrap_brokers }
