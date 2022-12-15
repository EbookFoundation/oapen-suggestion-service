class UserError extends Error {
  constructor(msg) {
    super(msg);
    this.message = msg;
    this.status = 400;
    this._catch = true;
  }
}

// RegEx to match formatting of handle
const handleRegExpression = new RegExp("([0-9]+.[0-9]+.[0-9]+/[0-9]+)", "g");

const checkHandle = async (handle) => {
  console.log(handle);
  console.log(typeof handle);
  if (!handle) throw new UserError("Handle must not be null");
  if (typeof handle !== "string")
    throw new UserError("Handle must be a string");
  if (!handle.includes("/")) throw new UserError("Invalid handle format");
  if (!handle.trim())
    throw new UserError("You must provide a handle and it must be non-empty");

  if (!handleRegExpression.test(handle.toString()))
    throw new UserError(
      `Invalid handle "${handle}", example format: 20.500.12657/47586`
    );
  return true;
};

module.exports = {
  checkHandle,
};
