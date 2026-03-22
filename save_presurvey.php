<?php
session_start();
require_once "db.php";

if (!isset($_SESSION["participant_id"])) {
    die("Participant session not found.");
}

$participant_id = $_SESSION["participant_id"];

$age_group = $_POST["age"] ?? "";
$digital_confidence = $_POST["confidence"] ?? "";
$digital_usage = $_POST["usage"] ?? "";
$suspicious_confidence = $_POST["identify"] ?? "";
$cyber_training = $_POST["training"] ?? "";
$pause_check = $_POST["pausecheck"] ?? "";
$urgency_trust = $_POST["urgency"] ?? "";
$authority_trust = $_POST["authority"] ?? "";
$pressure_confidence = $_POST["pressure"] ?? "";
$expected_performance = $_POST["performance"] ?? "";

$stmt = $conn->prepare("INSERT INTO presurvey (
    participant_id,
    age_group,
    digital_confidence,
    digital_usage,
    suspicious_confidence,
    cyber_training,
    pause_check,
    urgency_trust,
    authority_trust,
    pressure_confidence,
    expected_performance
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");

$stmt->bind_param(
    "sssssssssss",
    $participant_id,
    $age_group,
    $digital_confidence,
    $digital_usage,
    $suspicious_confidence,
    $cyber_training,
    $pause_check,
    $urgency_trust,
    $authority_trust,
    $pressure_confidence,
    $expected_performance
);

$stmt->execute();
$stmt->close();

header("Location: briefing.html");
exit();
?>