variable "project" {
  type        = string
  description = "Project name prefix"
  default     = "devops-portfolio"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "staging"
}

variable "location" {
  type        = string
  description = "Azure region"
  default     = "eastus"
}

variable "subscription_id" {
  type        = string
  description = "Azure subscription ID"
}

variable "tenant_id" {
  type        = string
  description = "Azure tenant ID"
}

variable "storage_account_name" {
  type        = string
  description = "Globally unique storage account name"
}

variable "vnet_cidr" {
  type        = string
  description = "CIDR for the VNet"
  default     = "10.20.0.0/16"
}

variable "ssh_source" {
  type        = string
  description = "Allowed CIDR for SSH"
  default     = "*"
}

variable "vm_size" {
  type        = string
  description = "VM size"
  default     = "Standard_B1s"
}

variable "admin_username" {
  type        = string
  description = "Admin username for the VM"
  default     = "azureuser"
}

variable "ssh_public_key" {
  type        = string
  description = "SSH public key for the VM"
}


