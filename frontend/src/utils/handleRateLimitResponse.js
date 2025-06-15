/**
 * Helper function to handle 429 Too Many Requests responses
 * @param {Response} response - The fetch Response object
 * @param {Function} setRateLimit - State setter for rate limit
 * @param {Function} setModal - State setter for modal display
 * @param {String} action - Description of the action being limited
 * @returns {Boolean} - Whether a 429 was handled (true) or not (false)
 */
export default function handleRateLimitResponse(
  response,
  setRateLimit,
  setModal,
  action = "request"
) {
  if (response.status === 429) {
    // Force client-side rate limiter to cooldown mode
    setRateLimit({
      attempts: 5,
      cooldown: true,
    });

    setModal({
      active: true,
      type: "fail",
      message: `Too many ${action} attempts. Please wait a few minutes before trying again.`,
    });

    return true;
  }

  return false;
}
