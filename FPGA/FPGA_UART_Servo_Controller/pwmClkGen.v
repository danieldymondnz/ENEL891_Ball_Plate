module pwmClkGen (input clk50MHz,
						output reg pwmClk);
						
	reg [7:0] count;
		
		always @ (posedge clk50MHz) begin
		// Was 194
			if (count > 117) begin
				count = 8'd0;
				pwmClk = !pwmClk;
			end
			else
				count = count + 8'd1;
		end
		
endmodule 