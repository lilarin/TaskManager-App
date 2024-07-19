document.addEventListener('DOMContentLoaded', function() {
  const StatusElement = document.querySelector('.task-detail-status');
  const deadlineElement = document.querySelector('.task-detail-deadline');

  if (StatusElement && deadlineElement) {
    const statusText = StatusElement.textContent;
    const deadlineText = deadlineElement.textContent;
    const { message, color } = formatStatus(statusText, deadlineText);

    StatusElement.textContent = message;
    StatusElement.style.color = color;
  }
});
