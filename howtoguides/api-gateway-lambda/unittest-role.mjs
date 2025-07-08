// roleValidator.test.mjs
import { validateRoles } from '../RoleValidator.mjs';

jest.mock('../GetManageServiceProviders.mjs', () => ({
  getManageServiceProviders: jest.fn(),
}));

const mockGetManageServiceProviders = require('../GetManageServiceProviders.mjs').getManageServiceProviders;

describe('validateRoles', () => {
  beforeEach(() => {
    jest.resetModules();
    process.env.SRE_CONFIGURED_ROLES = JSON.stringify(['sreRole1']);
    process.env.RDF_CONFIGURED_ROLES = JSON.stringify(['rdfRole1']);
  });

  it('should return false when no roles are in the token', async () => {
    const result = await validateRoles([], '/external-ids/resource', 'providerName', 'GET');
    expect(result).toBe(false);
  });

  it('should return true for matching SRE role on GET', async () => {
    const result = await validateRoles(['sreRole1'], '/external-ids/resource', 'providerName', 'GET');
    expect(result).toBe(true);
  });

  it('should return true for matching RDF role on GET', async () => {
    const result = await validateRoles(['rdfRole1'], '/external-ids/resource', 'providerName', 'GET');
    expect(result).toBe(true);
  });

  it('should return true for matching provider role on POST', async () => {
    const mockRoles = ['providerRole1'];
    mockGetManageServiceProviders.mockResolvedValueOnce(mockRoles);

    const result = await validateRoles(mockRoles, '/external-ids/resource', 'providerName', 'POST');
    expect(result).toBe(true);
  });

  it('should return false for non-matching roles on DELETE', async () => {
    mockGetManageServiceProviders.mockResolvedValueOnce(['providerRole1']);
    const result = await validateRoles(['randomRole'], '/external-ids/resource', 'providerName', 'DELETE');
    expect(result).toBe(false);
  });

  it('should return false for resources that do not include /external-ids', async () => {
    const result = await validateRoles(['rdfRole1'], '/other-resource', 'providerName', 'GET');
    expect(result).toBe(false);
  });

  it('should handle malformed RDF_CONFIGURED_ROLES gracefully', async () => {
    process.env.RDF_CONFIGURED_ROLES = 'rdfRole1,rdfRole2'; // Not JSON, fallback to split
    const result = await validateRoles(['rdfRole1'], '/external-ids/resource', 'providerName', 'GET');
    expect(result).toBe(true);
  });
});
