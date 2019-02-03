<?php
require('../include/php/config.php');
include("../".$BACKEND_FOLDER."include/php/db_c_n_f_g.php");
include("../".$BACKEND_FOLDER."include/php/cd14db.class.php");
$objDBCD14 = new CD14DB($DB_BASE, $DB_SERVER, $DB_USER, $DB_PASS);
include("../".$BACKEND_FOLDER."include/php/functions.php");
$ACTION = isset($_REQUEST['action']) ? check_input($_REQUEST['action'], $objDBCD14->dbh) : '';
$API_KEY = isset($_REQUEST['apiKey']) ? check_input($_REQUEST['apiKey'], $objDBCD14->dbh) : '';
$USER_NAME = isset($_REQUEST['userId']) ? check_input($_REQUEST['userId'], $objDBCD14->dbh) : '0';
$rs = $objDBCD14->queryUniqueObject("SELECT UserId, APIKey FROM tbl_users WHERE UserName = '".$USER_NAME."'");
$result = array('error'=> "nothing found");
if (isset($rs->UserId) && $rs->UserId != '')
{
	if(md5_decrypt($rs->APIKey) == $API_KEY)
	{
		$USER_ID = $rs->UserId;
		include("../".$BACKEND_FOLDER."include/php/crypt.php");
		$crypt = new crypt;
		$crypt->crypt_key($USER_ID);
		$rwCrncy = $objDBCD14->queryUniqueObject('SELECT CurrencyAbb, CurrencySymbol, ConversionRate, CurrencyId FROM tbl_currency WHERE DefaultCurrency = 1 AND 
					DisableCurrency = 0');
		if (isset($rwCrncy->CurrencyAbb) && $rwCrncy->CurrencyAbb != '')
		{
			$myCurrency = $rwCrncy->CurrencyAbb;
			$myCurrSymbol = $rwCrncy->CurrencySymbol;
			$CONVERSION_RATE = $rwCrncy->ConversionRate;
			$MY_CURRENCY_ID = $rwCrncy->CurrencyId;
		}
		$rwMyCrdts = $objDBCD14->queryUniqueObject("SELECT Credits, CurrencyAbb, CurrencySymbol, ConversionRate, A.CurrencyId FROM tbl_users A LEFT JOIN 
					tbl_currency B ON (A.CurrencyId = B.CurrencyId) WHERE UserId = '$USER_ID'");
		if (isset($rwMyCrdts->Credits) && $rwMyCrdts->Credits != '')
		{
			$myCredits = $crypt->decrypt($rwMyCrdts->Credits);
			$myCredits = number_format($myCredits, 2, '.', '');
		}
		if (isset($rwMyCrdts->CurrencyAbb) && $rwMyCrdts->CurrencyAbb != '')
		{
			$myCurrency = $rwMyCrdts->CurrencyAbb;
			$myCurrSymbol = $rwMyCrdts->CurrencySymbol;
			$CONVERSION_RATE = $rwMyCrdts->ConversionRate;
			$MY_CURRENCY_ID = $rwMyCrdts->CurrencyId;
			$DEFAULT_CURRENCY = $rwMyCrdts->DefaultCurrency;
		}
		if($myCredits == '')
			$myCredits = 0;
		$result = array('currency' => $myCurrency , 'currency_symbol'=> $myCurrSymbol,
		 'conversion_rate'=> $CONVERSION_RATE, 'currency_id'=>$MY_CURRENCY_ID, 'default' =>$DEFAULT_CURRENCY , 'credit'=> $myCredits);
	}
}
		
$objDBCD14->close();
echo json_encode($result) ;
?>