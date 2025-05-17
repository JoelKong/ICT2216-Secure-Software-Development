export default function formatTimestamp(timestamp) {
  // Format timestamp to relative time (e.g. "2 hours ago")
  try {
    const actualDate = new Date(timestamp);
    const now = new Date();
    const diffInMilliseconds = now - actualDate;

    // Convert to appropriate units
    const diffInMinutes = Math.floor(diffInMilliseconds / (1000 * 60));
    const diffInHours = Math.floor(diffInMilliseconds / (1000 * 60 * 60));
    const diffInDays = Math.floor(diffInMilliseconds / (1000 * 60 * 60 * 24));

    if (diffInMinutes < 1) {
      return "just now";
    } else if (diffInMinutes < 60) {
      return `${diffInMinutes} minute${diffInMinutes === 1 ? "" : "s"} ago`;
    } else if (diffInHours < 24) {
      return `${diffInHours} hour${diffInHours === 1 ? "" : "s"} ago`;
    } else {
      return `${diffInDays} day${diffInDays === 1 ? "" : "s"} ago`;
    }
  } catch (error) {
    return "recently";
  }
}
