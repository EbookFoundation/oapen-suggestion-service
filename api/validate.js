class UserError extends Error {
  constructor(msg) {
    super(msg)
    this.message = msg
    this.status = 400
    this._catch = true
  }
}

let checkHandle = async (handle) => {
  if(!handle) throw new UserError("Handle must not be null")
  if(typeof handle !== "string") throw new UserError("Handle must be a string")
  if(!handle.includes("/")) throw new UserError("Invalid handle format");
  // TODO: Validate the book's handle
  return true;
};

module.exports = {
  checkHandle,
};
