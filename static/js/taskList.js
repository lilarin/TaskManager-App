document.addEventListener('DOMContentLoaded', function() {
  const taskItems = document.querySelectorAll('.page-item-list');

  taskItems.forEach(taskItem => {
    const statusElement = taskItem.querySelector('.status');
    const deadlineElement = taskItem.querySelector('.publish-date');

    if (statusElement && deadlineElement) {
      const statusText = statusElement.textContent;
      const deadlineText = deadlineElement.textContent.split('-')[1].trim();
      const { message, color } = formatStatus(statusText, deadlineText);

      statusElement.textContent = message;
      statusElement.style.color = color;
    }
  });
});
