
export const checkAndGetEnv = (envName: string, errMsg?: string): string => {
  const envVar = process.env[envName];
  if (envVar === undefined) {
    const error = new Error(errMsg || `${envName} not found in environment variables`);
    console.error(error);
    throw error;
  }
  return envVar;
};
