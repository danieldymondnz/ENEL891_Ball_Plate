// baudClkGen 
// Generates a Baud Clock Rate based upon the 50 MHz Crystal on the DE0-Nano
// Ball Plate Project - Daniel Dymond, Sara Kinghan
// Using standardised Baud Rate of 9600 (more than ample samples)

module baudClkGen (	input clk50MHz,
							output reg baudClk);
							
		reg [19:0] count;
		
		always @ (posedge clk50MHz) begin
			if (count > 306748) begin
				count = 8'd0;
				baudClk = !baudClk;
			end
			else
				count = count + 8'd1;
		end
		
endmodule