function toggleFaq(button) {
    const answer = button.nextElementSibling;
    answer.classList.toggle('open');
    button.querySelector('.faq-icon').textContent = answer.classList.contains('open') ? '−' : '+';
}