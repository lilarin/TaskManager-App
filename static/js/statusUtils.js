function formatStatus(statusText, deadlineText) {
  let message;
  let color;

  if (statusText.includes('Pending')) {
    const deadlineDate = new Date(deadlineText);
    const currentDate = new Date();

    const timeDiff = deadlineDate - currentDate;
    const daysLeft = Math.ceil(timeDiff / (1000 * 3600 * 24));
    if (daysLeft > 1) {
      message = `Pending: ${daysLeft} days left`;
      if (daysLeft <= 3) {
        color = '#ff6174';
      }
    } else if (daysLeft === 1) {
      message = 'Pending: 1 day left';
      color = '#e83f21';
    } else if (daysLeft === 0) {
      message = 'Pending: Deadline is today';
      color = '#ff697a';
    } else {
      message = 'Pending: Deadline passed';
      color = '#ff001d';
    }
  } else {
    message = 'Completed';
    color = '#19c031';
  }

  return { message, color };
}
