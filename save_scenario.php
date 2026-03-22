<?php
session_start();
require_once "db.php";

if (!isset($_SESSION["participant_id"])) {
    die("Participant session not found.");
}

$participant_id = $_SESSION["participant_id"];

$round_number = isset($_POST["round_number"]) ? (int)$_POST["round_number"] : 0;
$scenario_number = isset($_POST["scenario_number"]) ? (int)$_POST["scenario_number"] : 0;
$cue_type = $_POST["cue_type"] ?? "";
$user_choice = $_POST["user_choice"] ?? "";
$is_correct = $_POST["is_correct"] ?? "";
$response_time = isset($_POST["response_time"]) ? (float)$_POST["response_time"] : 0;
$score_after_action = isset($_POST["score_after_action"]) ? (int)$_POST["score_after_action"] : 0;
$next_page = $_POST["next_page"] ?? "briefing.html";

$stmt = $conn->prepare("INSERT INTO scenario_results (
    participant_id,
    round_number,
    scenario_number,
    cue_type,
    user_choice,
    is_correct,
    response_time,
    score_after_action
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");

$stmt->bind_param(
    "siisssdi",
    $participant_id,
    $round_number,
    $scenario_number,
    $cue_type,
    $user_choice,
    $is_correct,
    $response_time,
    $score_after_action
);

$stmt->execute();
$stmt->close();

header("Location: " . $next_page);
exit();
?>