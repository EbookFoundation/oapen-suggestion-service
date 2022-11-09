let checkHandle = async (handle) => {
  if (!handle || typeof handle !== "string" || !handle.trim()) throw "Invalid handle, cannot be undefined.";
  if (!new RegExp('([0-9]+.[0-9]+.[0-9]+/[0-9]+)', 'g').test(handle)) throw "Invalid handle, exmaple format: 20.500.12657/47586"
  return true;
};

module.exports = {
  checkHandle,
};
