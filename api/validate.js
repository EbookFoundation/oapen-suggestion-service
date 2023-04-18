class UserError extends Error {
  constructor(msg) {
    super(msg);
    this.message = msg;
    this.status = 400;
    this._catch = true;
  }
}

const MAX_ITEM_LIMIT = 100;
const DEFAULT_ITEM_LIMIT = 25;

// RegEx to match formatting of handle
const handleRegExpression = new RegExp("([0-9]+.[0-9]+.[0-9]+/[0-9]+)");

let checkHandle = async (handle) => {
  if (!handle) throw new UserError("Handle must not be null");
  if (typeof handle !== "string")
    throw new UserError("Handle must be a string");
  if (!handle.includes("/")) throw new UserError("Invalid handle format");
  if (!handle || typeof handle !== "string" || !handle.trim())
    throw "Invalid handle, cannot be undefined.";
  if (!handleRegExpression.test(handle))
    throw "Invalid handle, exmaple format: 20.500.12657/47586";
  return true;
};

module.exports = {
  checkHandle,
  MAX_ITEM_LIMIT,
  DEFAULT_ITEM_LIMIT
};
