// baudClkGen 
// Generates a Baud Clock Rate based upon the 50 MHz Crystal on the DE0-Nano
// Ball Plate Project - Daniel Dymond, Sara Kinghan
// Using standardised Baud Rate of 9600 * 16 tick/sample (more than ample samples)

module baudClkGen (	input clk50MHz,
							output reg baudClk);
							
		reg [7:0] count;
		
		always @ (posedge clk50MHz) begin
			if (count > 162) begin
				count = 0;
				baudClk = !baudClk;
			end
			else
				count = count + 1;
		end
		
endmodule