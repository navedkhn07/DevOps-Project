output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
  description = "Resource Group name"
}

output "vm_public_ip" {
  value       = azurerm_public_ip.pip.ip_address
  description = "Public IP of the VM"
}

output "storage_account_name" {
  value       = azurerm_storage_account.sa.name
  description = "Storage account name"
}


