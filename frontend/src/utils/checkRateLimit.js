export default function checkRateLimit(rateLimit, setRateLimit, setModal) {
  // Check if rate limit reached
  if (rateLimit.cooldown) {
    const error =
      "Too many attempts. Please wait a short while before trying again.";
    setModal({
      active: true,
      type: "fail",
      message: error,
    });
    return true;
  }

  setRateLimit((prev) => {
    const updatedAttempts = prev.attempts + 1;
    return {
      attempts: updatedAttempts,
      cooldown: updatedAttempts >= 5,
    };
  });

  return false;
}
