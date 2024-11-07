// @ts-ignore
import buildTools from "node-gyp-build";
import path from "path";
import { fileURLToPath } from "url";

// Synthetically generate the __dirname for `mjs` cross support.
// Also gets the `../` of the dirname to get to the root of the project.
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(path.dirname(__filename));

const keytar = buildTools(__dirname)

function checkRequired(val: string, name: string) {
  if (!val || val.length <= 0) {
    throw new Error(name + " is required.");
  }
}

/**
 * Get the stored password for the service and account.
 *
 * @param service The string service name.
 * @param account The string account name.
 *
 * @returns A promise for the password string.
 */
export function getPassword(
  service: string,
  account: string
): Promise<string | null> {
  checkRequired(service, "Service");
  checkRequired(account, "Account");

  return keytar.getPassword(service, account);
}

/**
 * Add the password for the service and account to the keychain.
 *
 * @param service The string service name.
 * @param account The string account name.
 * @param password The string password.
 *
 * @returns A promise for the set password completion.
 */
export function setPassword(
  service: string,
  account: string,
  password: string
): Promise<void> {
  checkRequired(service, "Service");
  checkRequired(account, "Account");
  checkRequired(password, "Password");

  return keytar.setPassword(service, account, password);
}

/**
 * Delete the stored password for the service and account.
 *
 * @param service The string service name.
 * @param account The string account name.
 *
 * @returns A promise for the deletion status. True on success.
 */
export function deletePassword(
  service: string,
  account: string
): Promise<boolean> {
  checkRequired(service, "Service");
  checkRequired(account, "Account");

  return keytar.deletePassword(service, account);
}

/**
 * Find a password for the service in the keychain.
 *
 * @param service The string service name.
 *
 * @returns A promise for the password string.
 */
export function findPassword(service: string): Promise<string | null> {
  checkRequired(service, "Service");

  return keytar.findPassword(service);
}

/**
 * Find all accounts and passwords for `service` in the keychain.
 *
 * @param service The string service name.
 *
 * @returns A promise for the array of found credentials.
 */
export function findCredentials(
  service: string
): Promise<Array<{ account: string; password: string }>> {
  checkRequired(service, "Service");

  return keytar.findCredentials(service);
}
