
`timescale 1ps/1ps

module uart_Testbench();

	reg pskClk;
	reg rxInput;
	reg [7:0] rxDataOut;
	reg rxLEDFlag;
	
	uartReciever DUT_reciever(.I(pskClk), .I(rxInput), .sel(rxDataOut), .sel(rxLEDFlag));
	
	
	initial pskClk = 0;
	
	always #164 pskClk=~pskClk;

	initial begin
		rxInput = 1;
		
		// Delay by one frame
		rxInput = 0;
		#328
		
		
		// Delay by one frame
		rxInput = 1;
		#328
		
	
	end;
	
end module;