<?php
session_start();
require_once "db.php";

$participant_id = uniqid("CQ_", true);

$_SESSION["participant_id"] = $participant_id;

$stmt = $conn->prepare("INSERT INTO participants (participant_id) VALUES (?)");
$stmt->bind_param("s", $participant_id);
$stmt->execute();
$stmt->close();

header("Location: consent.html");
exit();
?>