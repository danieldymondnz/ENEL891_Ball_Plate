module pwmClkGen (input clk50MHz,
						output reg pwmClk);
						
	reg [9:0] count;
		
		always @ (posedge clk50MHz) begin
		// Was 194
			if (count > 586) begin
				count = 10'd0;
				pwmClk = !pwmClk;
			end
			else
				count = count + 10'd1;
		end
		
endmodule 