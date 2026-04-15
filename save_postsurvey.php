<?php
session_start();
require_once "db.php";

if (!isset($_SESSION["participant_id"])) {
    die("Participant session not found.");
}

$participant_id = $_SESSION["participant_id"];

$perceived_difficulty = $_POST["difficulty"] ?? "";
$perceived_pressure = $_POST["pressure"] ?? "";
$perceived_realism = $_POST["realism"] ?? "";
$perceived_engagement = $_POST["engagement"] ?? "";
$confidence_after = $_POST["confidence_after"] ?? "";
$decision_pressure = $_POST["decision_pressure"] ?? "";
$urgency_influence = $_POST["urgency_influence"] ?? "";
$qual_post1 = $_POST["qual_post1"] ?? "";
$qual_post2 = $_POST["qual_post2"] ?? "";
$qual_post3 = $_POST["qual_post3"] ?? "";

$stmt = $conn->prepare("INSERT INTO postsurvey (
    participant_id,
    perceived_difficulty,
    perceived_pressure,
    perceived_realism,
    perceived_engagement,
    confidence_after,
    decision_pressure,
    urgency_influence,
    qual_post1,
    qual_post2,
    qual_post3
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");

$stmt->bind_param(
    "sssssssssss",
    $participant_id,
    $perceived_difficulty,
    $perceived_pressure,
    $perceived_realism,
    $perceived_engagement,
    $confidence_after,
    $decision_pressure,
    $urgency_influence,
    $qual_post1,
    $qual_post2,
    $qual_post3
);

$stmt->execute();
$stmt->close();

header("Location: thankyou.html");
exit();
?>