/**
 *
 * @author Zach Johnson
 * @version 9/10/2021
 * The Quote class holds information about a stock's quote for the day 
 */
public class Quote {
    
    // declare class variables 
    private String ticker; 
    private int date; 
    private double open; 
    private double high; 
    private double low;
    private double close; 
    private int vol; 
    
    //overloaded constructor
    public Quote(String ticker, int date, double open, double high, double low, double close, int vol) {
        this.ticker = ticker;
        this.date = date;
        this.open = open;
        this.high = high;
        this.low = low;
        this.close = close;
        this.vol = vol;
    }
    
    // default constructor
     public Quote() {
    }
/**
 *   @return ticker name of stock 
 */
    public String getTicker() {
        return ticker;
    }
/**
 *   @return date of quote 
 */
    public int getDate() {
        return date;
    }
/**
 *   @return price of stock at days open 
 */
    public double getOpen() {
        return open;
    }
/**
 *   @return high price of stock on given day  
 */
    public double getHigh() {
        return high;
    }
/**
 *   @return low price of stock on given day 
 */
    public double getLow() {
        return low;
    }
/**
 *   @return 
 */
    public double getClose() {
        return close;
    }
/**
 *   @return volume of trades of stock 
 */
    public int getVol() {
        return vol;
    }
    /**
     * 
     * @param ticker name of stock
     */
    public void setTicker(String ticker) {
        this.ticker = ticker;
    }
/**
 * 
 * @param date of quote 
 */
    public void setDate(int date) {
        this.date = date;
    }
/**
 * 
 * @param open price of stock at open 
 */
    public void setOpen(double open) {
        this.open = open;
    }
/**
 * 
 * @param high max price of stock on given day 
 */
    public void setHigh(double high) {
        this.high = high;
    }
/**
 * 
 * @param low minimum price of stock on given day 
 */
    public void setLow(double low) {
        this.low = low;
    }
/**
 * 
 * @param close closing price of stock
 */
    public void setClose(double close) {
        this.close = close;
    }
/**
 * 
 * @param vol trading volume of stock 
 */
    public void setVol(int vol) {
        this.vol = vol;
    }
    
   /**
    * 
    * @param o Object to be compared 
    * @return truth value of equals method
    */
    public boolean equals( Object o )
    {
        if ( !( o instanceof Quote ) )
            return false;
        Quote e = ( Quote ) o;
        
        return ticker == e.getTicker()
                && date == e.getDate();
}
    /**
     * 
     * @return Quote object as a string
     */
     @Override
    public String toString() {
        return getTicker() +"@"+ getDate()+":"+getOpen()+":"+getHigh()+":"+getLow()+":"+getClose()+":"+getVol(); 
    }
}
