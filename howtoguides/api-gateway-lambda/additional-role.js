function getSREConfiguredRoles() {
  try {
    return JSON.parse(process.env.SRE_CONFIGURED_ROLES || '[]');
  } catch (e) {
    return (process.env.SRE_CONFIGURED_ROLES || '').split(',').map(r => r.trim()).filter(Boolean);
  }
}

function getRDFConfiguredRoles() {
  try {
    return JSON.parse(process.env.RDF_CONFIGURED_ROLES || '[]');
  } catch (e) {
    return (process.env.RDF_CONFIGURED_ROLES || '').split(',').map(r => r.trim()).filter(Boolean);
  }
}

export const validateRoles = async (rolesInToken, resource, providerName, httpMethod) => {
  const sreConfiguredRoles = getSREConfiguredRoles();
  const rdfConfiguredRoles = getRDFConfiguredRoles();

  console.log('***sreConfiguredRoles***:', sreConfiguredRoles);
  ...
};
