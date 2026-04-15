<?php
session_start();
require_once "db.php";

if (!isset($_SESSION["participant_id"])) {
    die("Participant session not found.");
}

$participant_id = $_SESSION["participant_id"];

$age_group = $_POST["age"] ?? "";
$gender = $_POST["gender"] ?? "";
$education_level = $_POST["education"] ?? "";
$cyber_training = $_POST["training"] ?? "";
$digital_usage = $_POST["usage"] ?? "";
$suspicious_confidence = $_POST["identify"] ?? "";
$qual1 = $_POST["qual1"] ?? "";
$qual2 = $_POST["qual2"] ?? "";
$qual3 = $_POST["qual3"] ?? "";
$qual4 = $_POST["qual4"] ?? "";

$stmt = $conn->prepare("INSERT INTO presurvey (
    participant_id,
    age_group,
    gender,
    education_level,
    cyber_training,
    digital_usage,
    suspicious_confidence,
    qual1,
    qual2,
    qual3,
    qual4
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");

$stmt->bind_param(
    "sssssssssss",
    $participant_id,
    $age_group,
    $gender,
    $education_level,
    $cyber_training,
    $digital_usage,
    $suspicious_confidence,
    $qual1,
    $qual2,
    $qual3,
    $qual4
);

$stmt->execute();
$stmt->close();

header("Location: briefing.html");
exit();
?>