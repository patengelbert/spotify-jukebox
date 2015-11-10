#include <errno.h>
#include <libgen.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>

#include <libspotify/api.h>

#include "audio.h"

#include <boost/interprocess/managed_shared_memory.hpp>
#include <boost/interprocess/containers/vector.hpp>
#include <boost/interprocess/allocators/allocator.hpp>


using namespace boost::interprocess

//Define an STL compatible allocator of ints that allocates from the managed_shared_memory.
//This allocator will allow placing containers in the segment
typedef allocator<int, managed_shared_memory::segment_manager>  ShmemAllocator;

//Alias a vector that uses the previous STL-like allocator so that allocates
//its values from the segment
typedef vector<int, ShmemAllocator> TrackQueue;

sp_track* getNextTrack()
{
//Remove shared memory on construction and destruction
     	struct shm_remove
      	{
        	shm_remove() { shared_memory_object::remove("TrackQueue"); }
         	~shm_remove(){ shared_memory_object::remove("TrackQueue"); }
      	} remover;

	managed_shared_memory segment(open_or_create, "TrackQueue", 65536);

	const ShmemAllocator alloc_inst (segment.get_segment_manager());

	TrackQueue *trackqueue = segment.construct<TrackQueue>("TrackQueue")(alloc_inst);
	
	trackqueue -> pop
}

