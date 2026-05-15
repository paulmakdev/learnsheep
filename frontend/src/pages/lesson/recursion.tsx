export default function Recursion() {
    return (
        <>
            <h3 style={{backgroundColor: "var(--tertiary-bg)", padding: "var(--smaller-padding)"}}>
                Idea
            </h3>
            <div  style={{paddingLeft: "var(--smaller-padding)", paddingRight: "var(--smaller-padding)"}}>
                <p>
                    Let's say we had some function, f(x) = x*x. If we wanted to find f(2), we would do f(2) = 2*2 = 4.
                </p>
                <p>
                    But what if we wanted to repeat the process twice? What would that look like?
                </p>
                <br></br>
                <p>
                    We can plug f(2) = 4 into the equation (simple substition): f(f(2)) = f(2*2) = f(4) = 4*4 = 16.
                </p>
                <br></br>
                <p>
                    Let's say that we were crazy and wanted to figure out what f(f(f(2))) was, or if we applied the function f three times in a row.
                </p>
                <p>
                    We get something like this: f(2) = 4 → f(4) = 16 → f(16) = 256.
                </p>
                <p>
                    But since we are professionals, we realize that we can apply the function f as many times as we want if we use a loop:
                </p>
                <br></br>
                <div style={{backgroundColor: "var(--fourth-bg)", color: "black", padding: "var(--standard-padding)"}}>
                    <p>initial_value = 2</p>
                    <p>times_to_repeat = 3</p>
                    <p>resultant_value=initial_value</p>
                    <p>for i in range(times_to_repeat):</p>
                    <p style={{paddingLeft: "var(--mini-padding)"}}>resultant_value=resultant_value*resultant_value</p>
                    <br></br>
                    <p>print resultant_value</p>
                </div>
                <p>
                    As you can see, we can easily find the result of applying f to any number as many times as we want using a loop.
                </p>
                <p>
                    But what if we wanted to stop when we reached a certain point? Let's say we want to stop when f(x) is greeater than 1000 or less than 0.5.
                </p>
                <p>
                    We could use a while loop, or conditional statement, sure, and that would work great.
                </p>
                <p>
                    But what if our function was just a liiiittle bit different? What if
                </p>
            </div>

        </>
    );
}
