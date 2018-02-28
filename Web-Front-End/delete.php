<?php
  include_once("conn.php");

  $engineer_mac = filter_var($_POST["nextTDs"], FILTER_SANITIZE_STRING);

  $sql_statement = $conn->prepare("DELETE FROM engineer_assignment WHERE board_id = ?");
  $sql_statement->bind_param("s", $engineer_mac);

  $result = $sql_statement->execute();
   // redirecciona a la página anterior
   header("Location:admin.php?iddrs=" . $iddrs);
?>
