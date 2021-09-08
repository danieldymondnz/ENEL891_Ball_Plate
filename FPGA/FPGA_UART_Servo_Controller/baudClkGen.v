// baudClkGen 
// Generates a Baud Clock Rate based upon the 50 MHz Crystal on the DE0-Nano
// Ball Plate Project - Daniel Dymond, Sara Kinghan
// Using standardised Baud Rate of 19200 * 16 tick/sample (more than ample samples)
// 50 MHz / 19200 / 16 / 2 - 1 = 80

module baudClkGen (	input clk50MHz,
							output reg baudClk);
							
		reg [6:0] count;
		
		always @ (posedge clk50MHz) begin
			if (count > 80) begin
				count = 0;
				baudClk = !baudClk;
			end
			else
				count = count + 1;
		end
		
endmodule