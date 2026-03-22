function goToBriefing() {
  const consentCheck = document.getElementById("consentCheck");
  const consentMessage = document.getElementById("consentMessage");

  if (consentCheck && consentCheck.checked) {
    window.location.href = "presurveyquestionnaire.html";
  } else if (consentMessage) {
    consentMessage.textContent = "You must provide consent before continuing.";
  }
}