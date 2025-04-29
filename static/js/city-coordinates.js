// 城市坐标数据
const cityCoordinates = {
    // 美国城市
    "Columbia, SC": [-81.0452, 33.9982],
    "Grand Rapids, MI": [-85.6681, 42.9634],
    "Augusta, GA": [-82.0105, 33.4709],
    "Birmingham, AL": [-86.8025, 33.5207],
    "Chicago, IL": [-87.6298, 41.8781],
    "New York, NY": [-74.0060, 40.7128],
    "San Francisco, CA": [-122.4194, 37.7749],
    "Denver, CO": [-104.9903, 39.7392],
    "Los Angeles, CA": [-118.2437, 34.0522],
    "Kansas City, KS": [-94.5786, 39.0997],
    "Memphis, TN": [-90.0490, 35.1495],
    "Nashville, TN": [-86.7816, 36.1627],
    "Knoxville, TN": [-83.9207, 35.9606],
    "Asheville, NC": [-82.5540, 35.5951],
    "Chapel Hill, NC": [-79.0558, 35.9132],
    "Raleigh, NC": [-78.6382, 35.7796],
    "Wilmington, NC": [-77.9447, 34.2257],
    "Charleston, SC": [-79.9311, 32.7765],
    "Cincinnati, OH": [-84.5120, 39.1031],
    "Holland, MI": [-86.1089, 42.7875],
    "Ann Arbor, MI": [-83.7430, 42.2808],
    "Baldwin, MI": [-85.8517, 43.9011],
    "Indianapolis, IN": [-86.1581, 39.7684],
    "Cleveland, OH": [-81.6944, 41.4993],
    "Pittsburgh, PA": [-79.9959, 40.4406],
    "Baltimore, MD": [-76.6122, 39.2904],
    "Washington DC, DC": [-77.0369, 38.9072],
    "Richmond, VA": [-77.4360, 37.5407],
    "Lynchburg, VA": [-79.1422, 37.4138],
    "Charlotte, NC": [-80.8431, 35.2271],
    "Greenville, SC": [-82.3940, 34.8526],
    "Atlanta, GA": [-84.3880, 33.7490],
    "Savannah, GA": [-81.0998, 32.0809],
    "Montgomery, AL": [-86.2999, 32.3668],
    "Tampa, FL": [-82.4572, 27.9506],
    "Orlando, FL": [-81.3792, 28.5383],
    "Miami, FL": [-80.1918, 25.7617],
    "Myrtle Beach, SC": [-78.8867, 33.6891],
    "Pensacola, FL": [-87.2169, 30.4213],
    "Panama City, FL": [-85.6602, 30.1588],
    "Wilmington, DE": [-75.5264, 39.7392],
    "Louisville, KY": [-85.7585, 38.2527],
    "Lexington, KY": [-84.4581, 38.0489],
    "Charleston, WV": [-81.6333, 38.3498],
    "Buffalo, NY": [-78.8784, 42.8864],
    "Ithaca, NY": [-76.5014, 42.4414],
    "Newark, NJ": [-74.1744, 40.7357],
    "Jersey City, NJ": [-74.0777, 40.7282],
    "Tupelo, MS": [-88.7036, 34.2577],
    "Chatanooga, TN": [-85.3097, 35.0456],
    "Jonesboro, AR": [-91.1403, 35.8423],
    "New Orleans, LA": [-90.0715, 29.9511],
    "Houston, TX": [-95.3698, 29.7604],
    "San Antonio, TX": [-98.4936, 29.4241],
    "Dallas, TX": [-96.7665, 32.7767],
    "Galveston, TX": [-94.7977, 29.3014],
    "San Jose, CA": [-121.8949, 37.3382],
    "Salt Lake City, UT": [-111.8910, 40.7608],
    "Warrensburg, MO": [-93.7322, 38.7492],
    "Seattle, WA": [-122.3321, 47.6062],
    "San Juan, PR": [-66.5901, 18.4663],
    

    
    //巴哈马
    "Nassau, BS": [-77.3435, 25.0581],
    "Freeport, BS": [-77.3514, 26.5299],
    
    

    // 加拿大城市
    "Toronto, ON": [-79.3832, 43.6532],
    "Montreal, QC": [-73.5673, 45.5017]
};

// 访问过的州列表（使用与地图数据匹配的州代码）
const visitedStates = new Set([
    "AL", // Alabama
    "AR", // Arkansas
    "CA", // California
    "CO", // Colorado
    "DC", // District of Columbia
    "DE", // Delaware
    "FL", // Florida
    "GA", // Georgia
    "IL", // Illinois
    "IN", // Indiana
    "KS", // Kansas
    "KY", // Kentucky
    "LA", // Louisiana
    "MD", // Maryland
    "MI", // Michigan
    "MO", // Missouri
    "MS", // Mississippi
    "NC", // North Carolina
    "NJ", // New Jersey
    "NY", // New York
    "OH", // Ohio
    "PA", // Pennsylvania
    "SC", // South Carolina
    "TN", // Tennessee
    "TX", // Texas
    "UT", // Utah
    "VA", // Virginia
    "WA", // Washington
    "WV", // West Virginia
    "ON", // Ontario
    "QC"  // Quebec
]); 